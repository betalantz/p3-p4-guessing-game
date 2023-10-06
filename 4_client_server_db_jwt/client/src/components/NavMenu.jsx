import { useState } from "react";
import { Menu, MenuItem, IconButton, Link } from "@mui/material";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import { Link as RouterLink } from "react-router-dom";
import { useAuth } from "../providers/authProvider";
import { logoutFetch } from "../api";

export default function NavMenu() {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const { token, setToken } = useAuth();

  const handleLogout = async () => {
    handleClose();
    const res = await logoutFetch();
    if (res.ok) setToken(null);
  };

  return (
    <div>
      <IconButton
        aria-label="more"
        id="menu-button"
        aria-controls="menu"
        aria-expanded={open ? "true" : undefined}
        aria-haspopup="true"
        onClick={handleClick}
      >
        <MoreVertIcon />
      </IconButton>
      <Menu
        id="menu"
        MenuListProps={{
          "aria-labelledby": "menu-button",
        }}
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
      >
          <MenuItem onClick={handleClose}>
            <Link component={RouterLink} to="/" underline="none">
              Dashboard
            </Link>
          </MenuItem>
          <MenuItem onClick={handleClose}>
            <Link component={RouterLink} to="/games/new" underline="none">
              New Game
            </Link>
          </MenuItem>
          <MenuItem onClick={handleLogout}>
            Logout
          </MenuItem>
    
      </Menu>
    </div>
  );
}
