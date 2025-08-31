import { createSlice } from '@reduxjs/toolkit';

interface AnalyticsState {
  reports: any[];
  trends: any[];
  metrics: any[];
  isLoading: boolean;
  error: string | null;
}

const initialState: AnalyticsState = {
  reports: [],
  trends: [],
  metrics: [],
  isLoading: false,
  error: null,
};

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    // Placeholder reducers - will be implemented with async thunks
  },
});

export default analyticsSlice.reducer;
