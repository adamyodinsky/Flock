import { ReactNode } from "react";
import Button from "./Button";

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
            <Button
              type="button"
              additionalClasses="btn-close"
              aria-label="Close"
              onClick={onClose}
            />
          </div>
          <div className="modal-body">{children}</div>
          <div className="modal-footer">
            <Button type="button" color="secondary" onClick={onClose}>
              Close
            </Button>
            {onSave && (
              <Button
                type="button"
                color="outline-primary"
                onClick={() => onSave()}
              >
                {saveButtonText}
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
