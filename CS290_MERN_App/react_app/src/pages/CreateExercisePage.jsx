import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const CreateExercisePage = () => {

    const [name, setName] = useState('');
    const [reps, setReps] = useState('');
    const [weight, setWeight] = useState('');
    const [unit, setUnit] = useState('');
    const [date, setDate] = useState('');

    const navigate = useNavigate();

    const addExercise = async () => {
        const newExercise = {name, reps, weight, unit, date}
        const response = await fetch(
            '/exercises', {
                method: 'POST',
                headers: {'Content-type': 'application/json'},
                body: JSON.stringify(newExercise)
            }
        );
        if (response.status === 201){
            alert("New exercise added!");
        } else {
            alert("Exercise not added. Failed with status code " + response.status)
        }
        navigate('/');
    };

    return (
        <div>
            <h2>Create Exercise</h2>
            <input
                type="text"
                placeholder="Exercise name"
                value={name}
                onChange={e => setName(e.target.value)} />
            <input
                type="number"
                placeholder="Reps hit"
                value={reps}
                onChange={e => setReps(e.target.valueAsNumber)} />
            <input
                type="number"
                placeholder="Weight per rep"
                value={weight}
                onChange={e => setWeight(e.target.valueAsNumber)} />
            <select name="unit" value={unit} onChange={e => setUnit(e.target.value)}>
                <option>Select one</option>
                <option value="lbs">lbs</option>
                <option value="kgs">kgs</option>
            </select>
            <input
                type="text"
                placeholder="Date in MM-DD-YY format"
                value={date}
                onChange={e => setDate(e.target.value)} />
            <button
                onClick={addExercise}
            >Add</button>
        </div>
    );
}

export default CreateExercisePage;