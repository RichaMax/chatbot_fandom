import { Box, Card, Divider, Paper, Stack } from "@mui/material";
import { useEffect, useRef } from "react";

export const ChatHistory = ({ chatRecords }: { chatRecords: ChatRecords }) => {
  const chatBottomRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatBottomRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatRecords]);

  return (
    <>
      <Paper
        style={{
          height: 600,
          overflow: "auto",
          display: "flex",
          flexDirection: "column",
        }}
        sx={{
          padding: 2,
          borderRadius: 3,
          border: 2,
        }}
      >
        <Box flexGrow={1} />
        <Stack spacing={2} direction="column">
          {chatRecords.map((record) => {
            return (
              <Card
                sx={{
                  padding: 1,
                  borderRadius: 3,
                  border: 2,
                }}
              >
                <Box>{record.question}</Box>
                <Divider sx={{ margin: 1 }} />
                <Box>{record.answer}</Box>
              </Card>
            );
          })}
        </Stack>
        <div ref={chatBottomRef}></div>
      </Paper>
    </>
  );
};
