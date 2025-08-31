import { createSlice } from '@reduxjs/toolkit';

interface MonitoringState {
  sessions: any[];
  content: any[];
  rules: any[];
  isLoading: boolean;
  error: string | null;
}

const initialState: MonitoringState = {
  sessions: [],
  content: [],
  rules: [],
  isLoading: false,
  error: null,
};

const monitoringSlice = createSlice({
  name: 'monitoring',
  initialState,
  reducers: {
    // Placeholder reducers - will be implemented with async thunks
  },
});

export default monitoringSlice.reducer;
