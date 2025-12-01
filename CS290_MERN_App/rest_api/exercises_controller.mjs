/**
 * Thomas (Tom) Haney
 */
import 'dotenv/config';
import express from 'express';
import asyncHandler from 'express-async-handler';
import * as exercises from './exercises_model.mjs';

const PORT = process.env.PORT;
const app = express();

app.use(express.json());

app.listen(PORT, async () => {
    await exercises.connect()
    console.log(`Server listening on port ${PORT}...`);
});


/**
 * 
 * @param {String} name 
 * @returns boolean (true if name is a string with at least one character)
 */
function isNameValid(name) {
    return typeof(name) === 'string' && name.length >= 1;
}

/**
 * 
 * @param {Number} reps 
 * @returns boolean (true if reps is an integer greater than 0)
 */
function isRepsValid(reps) {
    return typeof(reps) === 'number' && Number.isInteger(reps) && reps >= 1;
}

/**
 * 
 * @param {Number} weight 
 * @returns boolean (true if weight is an integer greater than 0)
 */
function isWeightValid(weight) {
    return typeof(weight) === 'number' && Number.isInteger(weight) && weight >= 1;
}

/**
 * 
 * @param {String} unit 
 * @returns boolean (true if unit is a string of exactly 'kgs' or 'lbs')
 */
function isUnitValid(unit) {
    return typeof(unit) === 'string' && (unit === 'kgs' || unit === 'lbs');
}

/**
*
* @param {string} date
* Return true if the date format is MM-DD-YY where MM, DD and YY are 2 digit integers
* Taken from the assignment page (just slightly modified by me)
*/
function isDateValid(date) {
    const format = /^\d\d-\d\d-\d\d$/;
    return typeof(date) === 'string' && format.test(date);
}

/**
 * Create a new user with query parameters passed by the body
 */
app.post('/exercises', asyncHandler(async (req, res) => {
    if (
        // Validate only 5 properties, and that they are all the ones we need
        Object.keys(req.body).length === 5 &&
        isNameValid(req.body.name) &&
        isRepsValid(req.body.reps) &&
        isWeightValid(req.body.weight) &&
        isUnitValid(req.body.unit) &&
        isDateValid(req.body.date)
    ) {
        // Create and insert the validated exercise
        const exercise = await exercises.createExercise(
            req.body.name,
            req.body.reps,
            req.body.weight,
            req.body.unit,
            req.body.date
        );
        res.status(201).json(exercise);
    } else {
        res.status(400).json({ Error: "Invalid request"});
    }
}));

/**
 * Retrieve all exercises in the database
 */
app.get('/exercises', asyncHandler(async (req, res) => {
    const all_exercises = await exercises.getAllExercises();
    res.status(200).json(all_exercises);
}));

/**
 * Retrieve one exercise with a matching _id
 */
app.get('/exercises/:_id', asyncHandler(async (req, res) => {
    const match = await exercises.findExerciseById({_id: req.params._id});
    // If we receive null, no matching exercise with the id was found
    if (match === null) {
        res.status(404).json({ Error: "Not found"});
    }
    res.status(200).json(match);
}));

/**
 * Update a specific exercise with _id with parameters in the body of the request
 */
app.put('/exercises/:_id', asyncHandler(async (req, res) => {
    if (
        // Validate only 5 properties, and that they are all the ones we need
        Object.keys(req.body).length === 5 &&
        isNameValid(req.body.name) &&
        isRepsValid(req.body.reps) &&
        isWeightValid(req.body.weight) &&
        isUnitValid(req.body.unit) &&
        isDateValid(req.body.date)
    ) {
        const match = await exercises.findExerciseById({_id: req.params._id});
        // If we receive null, no matching exercise with the id was found
        if (match === null) {
            res.status(404).json({ Error: "Not found"});
        }

        await exercises.updateExerciseById({_id: req.params._id}, {
            name: req.body.name,
            reps: req.body.reps,
            weight: req.body.weight,
            unit: req.body.unit,
            date: req.body.date
        });

        const updated = await exercises.findExerciseById({_id: req.params._id});
        res.status(200).json(updated);
    } else {
        res.status(400).json({ Error: "Invalid request"});
    }
    
}));

/**
 * Delete a specific exercise with _id
 */
app.delete('/exercises/:_id', asyncHandler(async (req, res) => {
    // Delete a user with the matching id
    const deleted = await exercises.deleteExerciseByFilter({_id: req.params._id});
    // If no users deleted, return a 404 with a not found object
    if (deleted.deletedCount === 0) {
        res.status(404).json({ Error: "Not found"});
    }
    // If successful, return 204 with no content
    res.status(204).send();
}));