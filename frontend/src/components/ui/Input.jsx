export default function Input({ label, id, ...props }) {
    return (
        <div className="ui-input-wrapper">
            <label className="ui-input-label" htmlFor={id}>
                {label}
            </label>
            <input className="ui-input" id={id} {...props} />
        </div>
    );
}