import { TextField } from "@mui/material";
import React from "react";

export const ChatInput = ({
  onQuestion,
  value,
  setValue,
  isQuestionPending,
}: {
  onQuestion: ({ question }: { question: string }) => void;
  value: string;
  setValue: (value: string) => void;
  isQuestionPending: boolean;
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
        endAdornment: isQuestionPending
          ? "Pending ..."
          : value
            ? "Send"
            : undefined,
        sx: {
          borderRadius: 3,
          border: 2,
        },
      }}
      onKeyDown={(e) => {
        if (e.key === "Enter") {
          onQuestion({ question: value });
          setValue("");
          e.preventDefault();
        }
      }}
    />
  );
};
