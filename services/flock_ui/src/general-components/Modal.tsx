import { ReactNode } from "react";
import Button from "./Button";

interface Props {
  title: string | undefined;
  children: ReactNode;
  showModal: boolean;
  extraClassNames?: string;
  onClose: () => void;
  footerButtons?: ReactNode;
}
const Modal = ({
  onClose,
  showModal,
  title,
  children,
  extraClassNames,
  footerButtons,
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
          <div className="modal-footer">{footerButtons}</div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
