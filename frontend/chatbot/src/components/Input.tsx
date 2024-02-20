import { TextField } from "@mui/material";
import React from "react";

export const ChatInput = ({
  onQuestion,
  value,
  setValue,
}: {
  onQuestion: (question: string) => void;
  value: string;
  setValue: (value: string) => void;
}) => {
  return (
    <TextField
      focused={false}
      fullWidth={true}
      value={value}
      onChange={(event) => setValue(event.target.value)}
      id="chat-input"
      placeholder="Type your question here"
      variant="outlined"
      InputProps={{
        endAdornment: value ? "Send" : undefined,
        sx: {
          borderRadius: 3,
          border: 2,
        },
      }}
      onKeyDown={(e) => {
        if (e.key === "Enter") {
          onQuestion(value);
          setValue("");
          e.preventDefault();
        }
      }}
    />
  );
};
