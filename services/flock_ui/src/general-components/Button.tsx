import { ReactNode } from "react";

interface Props {
  children?: ReactNode;
  color?:
    | "primary"
    | "secondary"
    | "success"
    | "danger"
    | "warning"
    | "info"
    | "light"
    | "dark"
    | "outline-primary"
    | "outline-secondary"
    | "outline-success"
    | "outline-danger"
    | "outline-warning"
    | "outline-info"
    | "outline-light"
    | "outline-dark";
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  type?: "submit" | "button" | "reset";
  disabled?: boolean;
  additionalClasses?: string;
  "aria-label"?: string;
  id?: string;
}

function Button({
  onClick,
  children,
  color = "primary",
  type = "button",
  disabled = false,
  additionalClasses = "",
  "aria-label": ariaLabel,
  id,
}: Props) {
  return (
    <button
      type={type}
      className={`btn btn-${color} ${additionalClasses}`}
      onClick={onClick}
      disabled={disabled}
      aria-label={ariaLabel}
      id={id}
    >
      {children}
    </button>
  );
}

export default Button;
