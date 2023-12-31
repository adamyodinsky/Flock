import { ReactNode } from "react";

interface Props {
  title: string | undefined;
  children: ReactNode;
  showModal: boolean;
  saveButtonText?: string;
  extraClassNames?: string;
  onClose: () => void;
  onSave?: () => void;
}
const Modal = ({
  onClose,
  onSave,
  showModal,
  title,
  children,
  saveButtonText,
  extraClassNames,
}: Props) => {
  if (!showModal) return null;

  return (
    <div
      className={`modal show ${extraClassNames}`}
      style={{ display: "block" }}
    >
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">{title}</h5>
            <button
              type="button"
              className="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
              onClick={onClose}
            ></button>
          </div>
          <div className="modal-body">{children}</div>
          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-secondary"
              data-bs-dismiss="modal"
              onClick={onClose}
            >
              Close
            </button>
            {onSave && (
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => onSave()}
              >
                {saveButtonText}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
