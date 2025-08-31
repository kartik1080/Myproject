import React from 'react';
import { Box, Typography, Card, CardContent, Paper } from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';

const Detection: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 4 }}>
        Drug Detection Management
      </Typography>
      
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <SearchIcon sx={{ fontSize: 80, color: 'primary.main', mb: 2 }} />
        <Typography variant="h5" gutterBottom>
          Detection System
        </Typography>
        <Typography variant="body1" color="text.secondary">
          This page will contain drug detection patterns, results, and management tools.
        </Typography>
      </Paper>
    </Box>
  );
};

export default Detection;
