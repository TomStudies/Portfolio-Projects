import { useEffect, useState } from 'react';
import ExerciseTable from '../components/ExerciseTable';
import { useNavigate } from 'react-router-dom';

function HomePage({setExerciseToEdit}) {
    const [exercises, setExercises] = useState([]);
    const navigate = useNavigate();

    const loadExercises = async () => {
        const response = await fetch('/exercises')
        const data = await response.json();
        setExercises(data)
    }

    useEffect( () => {
        loadExercises();
    }, []);

    const onDelete = async (_id) => {
        await fetch(`/exercises/${_id}`, {method: 'DELETE'});
        setExercises(exercises.filter(e => e._id !== _id));
    }

    const onEdit = (exercise) =>{
        setExerciseToEdit(exercise);
        navigate('/edit-exercise');
    }

    return (
        <>
            <h2>Home Page</h2>
            <ExerciseTable exercises={exercises} onDelete={onDelete} onEdit={onEdit}></ExerciseTable>
        </>
    );
}

export default HomePage;