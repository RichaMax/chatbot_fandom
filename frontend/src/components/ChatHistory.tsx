import { Box, Card, Divider, Paper, Stack } from "@mui/material";
import axios from "axios";
import { useEffect, useRef, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import Markdown from "react-markdown";

const ChatRecord = ({ game, question }: { game: string; question: string }) => {
  const { answer, setAnswer } = useState(undefined);
  const mutation = useMutation({
    mutationFn: async () => {
      return await axios.post("http://localhost:8013/ask", {
        question: question,
        game: game,
      });
    },
  });

  return (
    <Card
      sx={{
        padding: 1,
        borderRadius: 3,
        border: 2,
      }}
    >
      <Box>{question}</Box>
      <Divider sx={{ margin: 1 }} />
      {/* <Box>{mutation.isPending ? "..." : mutation.data?.answer}</Box> */}
    </Card>
  );
};

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
            // return <ChatRecord game={game} question={record.question} />;
            return (
              <>
                <Stack direction="row" justifyContent="end">
                <Card
                  sx={{
                    padding: 1,
                    borderRadius: 3,
                    border: 2,
                    maxWidth: "70%",
                  }}
                >
                  <Box>{record.question}</Box>
                </Card>
                </Stack>
                  <Card
                    sx={{
                      padding: 1,
                      borderRadius: 3,
                      border: 2,
                      maxWidth: "70%",
                    }}
                  >
                    <Box>
                      <Markdown>{record.answer}</Markdown>
                    </Box>
                  </Card>
              </>
            );
          })}
        </Stack>
        <div ref={chatBottomRef}></div>
      </Paper>
    </>
  );
};
