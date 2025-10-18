import { Box, MenuItem, Select, Tooltip } from "@mui/material";

type Game = {
  id: string;
  name: string;
  image: string;
};

const GameLogo = ({ game }: { game: Game }) => {
  return (
    <Tooltip title={game.name}>
      <Box
        sx={{
          height: 40,
          width: 40,
        }}
        component="img"
        src={game.image}
        paddingX={1}
      />
    </Tooltip>
  );
};

export const GameSelector = ({
  game,
  changeGame,
  availableGames,
}: {
  game: string;
  changeGame: (game: string) => void;
  availableGames: Game[];
}) => {
  return (
    <Select
      value={game}
      onChange={(event) => changeGame(event.target.value)}
      defaultValue="valheim"
      sx={{
        border: 2,
        borderRadius: 3,
      }}
    >
      {availableGames.map((game) => {
        return (
          <MenuItem value={game.id}>
            <Box display="flex" alignItems="center">
              <GameLogo game={game} />
              {game.name}
            </Box>
          </MenuItem>
        );
      })}
    </Select>
  );
};
