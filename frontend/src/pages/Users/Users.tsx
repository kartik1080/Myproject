import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { People as PeopleIcon } from '@mui/icons-material';

const Users: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 4 }}>
        User Management
      </Typography>
      
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <PeopleIcon sx={{ fontSize: 80, color: 'primary.main', mb: 2 }} />
        <Typography variant="h5" gutterBottom>
          User Management System
        </Typography>
        <Typography variant="body1" color="text.secondary">
          This page will contain user management, roles, and permissions.
        </Typography>
      </Paper>
    </Box>
  );
};

export default Users;
