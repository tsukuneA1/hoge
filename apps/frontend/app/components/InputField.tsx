type InputFieldProps = {
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  onCompositionStart?: (e: React.CompositionEvent) => void;
  onCompositionEnd?: (e: React.CompositionEvent) => void;
  onKeyDown?: (e: React.KeyboardEvent) => void;
  suffix?: string;
  type?: "text" | "number";
};

export const InputField = ({
  placeholder,
  value,
  onChange,
  onCompositionStart,
  onCompositionEnd,
  onKeyDown,
  suffix,
  type = "text",
}: InputFieldProps) => {
  return (
    <div className="flex items-center gap-2">
      <div className="bg-surface-primary border border-secondary rounded-xl px-4 py-3 flex items-center h-12 w-full">
        <input
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={(e) => onChange?.(e.target.value)}
          onCompositionStart={onCompositionStart}
          onCompositionEnd={onCompositionEnd}
          onKeyDown={(e) => onKeyDown?.(e)}
          className="flex-1 outline-none text-body-m text-primary placeholder:text-text-placeholder bg-transparent"
        />
      </div>
      {suffix && <span className="text-body-m text-primary">{suffix}</span>}
    </div>
  );
};

export default InputField;
