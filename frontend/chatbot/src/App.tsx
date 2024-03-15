import { useState } from "react";
import "./App.css";
import { ChatInput } from "./components/Input";
import { ChatHistory } from "./components/ChatHistory";
import { Box, Stack } from "@mui/material";
import valheim from "./assets/valheim.png";
import vrising from "./assets/vrising.png";
import { GameSelector } from "./components/GameSelector";
import axios from "axios";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { v4 as uuidv4 } from "uuid";

const getOrSetSessionId = () => {
  if (window.sessionStorage.getItem("sessionId") === null) {
    window.sessionStorage.setItem("sessionId", uuidv4());
  }
  return window.sessionStorage.getItem("sessionId");
};

function App() {
  const [game, setGame] = useState<string>("valheim");
  const [chatInput, setChatInput] = useState<string>("");

  const queryClient = useQueryClient();

  const sessionId = getOrSetSessionId();

  const askQuestionMutation = useMutation({
    mutationFn: async ({ question }: { question: string }) => {
      return await axios.post(
        "http://localhost:8013/ask",
        {
          question: question,
          game: game,
        },
        {
          headers: {
            "session-id": sessionId,
          },
        },
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["chatRecords", game] });
    },
  });

  const historyResponse = useQuery({
    queryKey: ["chatRecords", game],
    queryFn: async () =>
      axios.get(`http://localhost:8013/games/${game}/history`, {
        headers: {
          "session-id": sessionId,
        },
      }),
  });

  const chatRecords = historyResponse.data?.data.records;

  const handleChangeGame = (game: string) => {
    setGame(game);
  };

  return (
    <>
      <Box display="flex" alignItems="center" padding={1}>
        <Box flexGrow={1}></Box>
        <Box>
          <GameSelector
            game={game}
            changeGame={handleChangeGame}
            availableGames={[
              { id: "valheim", name: "Valheim", image: valheim },
              { id: "vrising", name: "V-Rising", image: vrising },
            ]}
          />
        </Box>
      </Box>
      <Stack spacing={2}>
        <ChatHistory chatRecords={chatRecords} />
        <ChatInput
          onQuestion={askQuestionMutation.mutate}
          value={chatInput}
          setValue={setChatInput}
          isQuestionPending={askQuestionMutation.isPending}
        />
      </Stack>
    </>
  );
}

export default App;
