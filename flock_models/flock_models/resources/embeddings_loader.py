"""Module for loading embeddings to vectorstore."""

import json
import os
from typing import Dict, List, Optional

from flock_schemas.base import Kind
from flock_schemas.embeddings_loader import EmbeddingsLoaderSchema
from langchain.docstore.document import Document
from langchain.document_loaders import CSVLoader, PDFMinerLoader, TextLoader

from flock_models.resources.base import Resource, ToolResource
from flock_models.resources.embedding import EmbeddingResource
from flock_models.resources.splitter import SplitterResource
from flock_models.resources.vectorstore import VectorStoreResource


class EmbeddingsLoaderResource(Resource):
    """Class for loading embeddings to vectorstore.

    Attributes:
        source_directory: Path to the directory with embeddings.
        base_meta_source: Path to the directory with metadata.
        archive_path: Path to the directory where embeddings will be archived.
        splitter: Splitter resource.
        embedding: Embedding resource.
        vectorstore: Vectorstore resource.
        allowed_extensions: List of allowed extension files (plain text loading only).
        deny_extensions: List of denied extension files (plain text loading only).
    """

    def __init__(
        self,
        manifest: EmbeddingsLoaderSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
    ) -> None:
        super().__init__(manifest, dependencies, tools)

        self.source_directory = (
            os.environ.get("SOURCE_DIRECTORY", None)
            or manifest.spec.options.source_directory
        )

        self.archive_path = (
            os.environ.get("ARCHIVE_PATH", None) or manifest.spec.options.archive_path
        )

        self.base_meta_source = (
            os.environ.get("BASE_META_SOURCE", None)
            or manifest.spec.options.base_meta_source
        )

        allowed_extensions = (
            os.environ.get("ALLOWED_EXTENSIONS", None)
            or manifest.spec.options.allowed_extensions
        )

        deny_extensions = (
            os.environ.get("DENY_EXTENSIONS", None)
            or manifest.spec.options.deny_extensions
        )

        if allowed_extensions:
            self.allowed_extensions = allowed_extensions.split(",")
        else:
            self.allowed_extensions = []

        if deny_extensions:
            self.deny_extensions = deny_extensions.split(",")
        else:
            self.deny_extensions = []

        self.splitter: SplitterResource = self.dependencies.get(Kind.Splitter)  # type: ignore
        self.embedding: EmbeddingResource = self.dependencies.get(Kind.Embedding)  # type: ignore
        self.vectorstore: VectorStoreResource = self.dependencies.get(Kind.VectorStore)  # type: ignore

    def _list_files_recursive(self, folder: str):
        """List all files in a folder recursively."""

        file_list = []

        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder)
                file_list.append(relative_path)

        return file_list

    @staticmethod
    def get_file_subpath(path):
        """Get subpath of a file."""
        path_parts = path.split(os.sep)
        return os.path.join(path_parts[-2], path_parts[-1])

    def _get_files_list(self, path: str):
        files = os.listdir(path)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))

        return files

    def _filter_files_by_allowed_extensions(self, files: list):
        if self.allowed_extensions == []:
            return files

        filtered_files = [
            file
            for file in files
            if os.path.splitext(file)[1] in self.allowed_extensions
        ]
        return filtered_files

    def _filter_files_by_deny_extensions(self, files: list):
        if self.deny_extensions == []:
            return files

        filtered_files = [
            file
            for file in files
            if os.path.splitext(file)[1] not in self.deny_extensions
        ]
        return filtered_files

    def _load_json(self, file_name: str):
        json_obj = []

        try:
            with open(file=file_name, mode="r", encoding="utf-8") as file:
                json_obj = json.load(file)
        except Exception as error:
            print(f"Error: {error}")

        return json_obj

    class FlockTextLoader(TextLoader):
        """Load text file from local storage."""

        def __init__(
            self,
            file_path: str,
            encoding: Optional[str] = None,
            base_meta_source: str = "",
        ):
            super().__init__(file_path, encoding)
            self.base_meta_source = base_meta_source

        def load(self) -> List[Document]:
            with open(file=self.file_path, mode="r", encoding="utf-8") as file:
                text = file.read()

            return [
                Document(
                    page_content=text,
                    metadata={
                        "source": f"{self.base_meta_source}/{EmbeddingsLoaderResource.get_file_subpath(file)}"
                    },
                )
            ]

    def load_single_document(self, file_path: str) -> Document:
        """Load a single document from a file path."""
        if file_path.endswith(".pdf"):
            loader = PDFMinerLoader(file_path)
        elif file_path.endswith(".csv"):
            loader = CSVLoader(file_path)
        else:
            loader = self.FlockTextLoader(
                file_path, encoding="utf8", base_meta_source=self.base_meta_source
            )

        return loader.load()[0]

    def load_scraped_data_to_vectorstore(self):
        """Load scraped data to vectorstore."""

        if not os.path.exists(self.source_directory):
            os.makedirs(self.source_directory)

        if not os.path.exists(self.archive_path):
            os.makedirs(self.archive_path)

        files = self._get_files_list(self.source_directory)

        for file in files:
            print(f"Loading {file} to vectorstore...")
            json_obj = self._load_json(f"{self.source_directory}/{file}")

            for page in json_obj:
                document = [
                    Document(
                        page_content=page["text"], metadata={"source": page["url"]}
                    )
                ]
                document = self.splitter.resource.split_documents(document)
                self.vectorstore.resource.add_documents(document)
                print(f"Added {page['url']} to the vectorstore.")

            # move file to archive
            print(f"Moving {file} to archive...")
            os.rename(f"{self.source_directory}/{file}", f"{self.archive_path}/{file}")

    def load_files_to_vectorstore(self):
        """Load plain text data to vectorstore."""

        if not os.path.exists(self.source_directory):
            os.makedirs(self.source_directory)

        if not os.path.exists(self.archive_path):
            os.makedirs(self.archive_path)

        files = self._list_files_recursive(self.source_directory)

        files = self._filter_files_by_allowed_extensions(files)
        files = self._filter_files_by_deny_extensions(files)

        for file in files:
            print(f"Adding {file} to the vectorstore.")

            document = self.load_single_document(f"{self.source_directory}/{file}")
            document = self.splitter.resource.split_documents([document])
            self.vectorstore.resource.add_documents(document)

            print(f"Moving {file} to archive...")
            os.rename(
                f"{self.source_directory}/{file}",
                f"{self.archive_path}/{os.path.basename(file)}",
            )
