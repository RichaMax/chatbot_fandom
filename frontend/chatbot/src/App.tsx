import { useState } from "react";
import "./App.css";
import { ChatInput } from "./components/Input";
import { ChatHistory } from "./components/ChatHistory";
import { Box, Stack } from "@mui/material";
import valheim from "./assets/valheim.png";
import vrising from "./assets/vrising.png";
import { GameSelector } from "./components/GameSelector";
import axios from "axios";

function App() {
  const [game, setGame] = useState<string>("valheim");
  const [chatRecords, setChatRecords] = useState<ChatRecords>([]);
  const [chatInput, setChatInput] = useState<string>("");

  const handleNewQuestion = async (question: string) => {
    const response = await axios.post("http://localhost:8000/ask", {
      question: question,
    });

    const newRecord: ChatRecord = {
      question: question,
      answer: response.data.answer,
      timestamp: Date.now(),
    };

    setChatRecords([...chatRecords, newRecord]);
  };

  const handleChangeGame = (game: string) => {
    setGame(game);

    setChatRecords([]);
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
          onQuestion={handleNewQuestion}
          value={chatInput}
          setValue={setChatInput}
        />
      </Stack>
    </>
  );
}

export default App;
