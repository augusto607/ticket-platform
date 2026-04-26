export default function Button({
    children,
    type = "button",
    variant = "primary",
    disabled = false,
    ...props
}) {
    return (
        <button
            type={type}
            className={`ui-button ui-button--${variant}`}
            disabled={disabled}
            {...props}
        >
            {children}
        </button>
    );
}