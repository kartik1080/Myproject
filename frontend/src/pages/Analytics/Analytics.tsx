import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { Analytics as AnalyticsIcon } from '@mui/icons-material';

const Analytics: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 4 }}>
        Analytics & Reporting
      </Typography>
      
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <AnalyticsIcon sx={{ fontSize: 80, color: 'primary.main', mb: 2 }} />
        <Typography variant="h5" gutterBottom>
          Analytics Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          This page will contain comprehensive analytics, reports, and data visualization tools.
        </Typography>
      </Paper>
    </Box>
  );
};

export default Analytics;
