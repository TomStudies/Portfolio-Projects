import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import CreateExercisePage from './pages/CreateExercisePage';
import EditExercisePage from './pages/EditExercisePage';
import Navigation from './components/Navigation';
import Head from './components/Head';
import Foot from './components/Foot';
import { useState } from 'react';

function App() {

  const [exerciseToEdit, setExerciseToEdit] = useState();

  return (
    <div className="app">
        <Router>
          <Head />
          <Routes>
            <Route path="/" element={<HomePage setExerciseToEdit={setExerciseToEdit}/>}></Route>
            <Route path="/create-exercise" element={ <CreateExercisePage />}></Route>
            <Route path="/edit-exercise" element={ <EditExercisePage exerciseToEdit={exerciseToEdit}/>}></Route>
          </Routes>
          <Navigation />
          <Foot />
        </Router>
    </div>
  );
}

export default App;
