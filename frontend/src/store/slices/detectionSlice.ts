import { createSlice } from '@reduxjs/toolkit';

interface DetectionState {
  detections: any[];
  patterns: any[];
  categories: any[];
  isLoading: boolean;
  error: string | null;
}

const initialState: DetectionState = {
  detections: [],
  patterns: [],
  categories: [],
  isLoading: false,
  error: null,
};

const detectionSlice = createSlice({
  name: 'detection',
  initialState,
  reducers: {
    // Placeholder reducers - will be implemented with async thunks
  },
});

export default detectionSlice.reducer;
