import {FaTrashAlt} from 'react-icons/fa';
import {HiPencilSquare} from 'react-icons/hi2';

function ExerciseRow({exercise, onDelete, onEdit}) {

    return (
        <tr>
            <td>{exercise.name}</td>
            <td>{exercise.reps}</td>
            <td>{exercise.weight}</td>
            <td>{exercise.unit}</td>
            <td>{exercise.date}</td>
            <td>
                <HiPencilSquare onClick={e => {onEdit(exercise)}}/>
            </td>
            <td>
                <FaTrashAlt onClick={e => {onDelete(exercise._id)}}/>
            </td>
        </tr>
    )
}

export default ExerciseRow;