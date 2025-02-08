import React from 'react';
import ReactDOM from 'react-dom/client'; // For React 18 and above
import AppServices from './AppServices';

// Create a root.
const root = ReactDOM.createRoot(document.getElementById('root'));

// Initial render
root.render(
  <React.StrictMode>
    <AppServices />
  </React.StrictMode>
); 