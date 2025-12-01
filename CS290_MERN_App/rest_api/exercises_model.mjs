/**
 * Thomas (Tom) Haney
 */
import mongoose from 'mongoose';
import 'dotenv/config';

const EXERCISE_DB_NAME = 'exercise_db';
const EXERCISE_CLASS_NAME = 'Exercise';

let connection = undefined;

/**
 * This function connects to the MongoDB server and to the database
 *  'exercise_db' in that server.
 */
async function connect(){
    try{
        connection = await mongoose.connect(process.env.MONGODB_CONNECT_STRING, 
                {dbName: EXERCISE_DB_NAME});
        console.log("Successfully connected to MongoDB using Mongoose!");
    } catch(err){
        console.log(err);
        throw Error(`Could not connect to MongoDB ${err.message}`)
    }
}

/**
 * Create the schema to be used for the exercises
 */
const exerciseSchema = mongoose.Schema({
    name: {type: String, required: true},
    reps: {type: Number, required: true},
    weight: {type: Number, required: true},
    unit: {type: String, required: true},
    date: {type: String, required: true}
});

/**
 * Create a model from the schema
 */
const Exercise = mongoose.model(EXERCISE_CLASS_NAME, exerciseSchema);

/**
 * Create a user
 * @param {String} name
 * @param {Number} reps 
 * @param {Number} weight
 * @param {String} unit
 * @param {String} date 
 * @returns A promise. Resolves to the JSON object for the exercise created by calling save
 */
const createExercise = async (name, reps, weight, unit, date) => {
    // Call the constructor to create an instance of the model class User
    const exercise = new Exercise({name: name, reps: reps, weight: weight, unit: unit, date: date});
    // Call save to persist this object as a document in MongoDB
    return exercise.save();
}

/**
 * Retrieves all exercises 
 * @returns A promise, which resolves to a JSON array containing all exercises
 */
const getAllExercises = async () => {
    const query = Exercise.find({});
    return query.exec();
}

/**
 * Find an exercise which matches filter (should only have _id)
 * @param {Object} filter 
 * @returns A promise, which resolves to a JSON object which matched _id (or null)
 */
const findExerciseById = async (filter) => {
    const query = Exercise.findOne(filter);
    return query.exec();
}

/**
 * Update the values of an exercise which matches filter (should only have _id)
 * @param {Object} filter 
 * @param {Object} update 
 * @returns A promise, which resolves to a JSON object with information about the update
 */
const updateExerciseById = async (filter, update) => {
    const query = Exercise.updateOne(filter, update);
    return query.exec();
}

/**
 * Delete the entry for a user which matches filter (can either be a complex filter or just _id)
 * @param {Object} filter 
 * @returns A promise, which resolves to a JSON object with information about the delete
 */
const deleteExerciseByFilter = async (filter) => {
    const query = Exercise.deleteMany(filter);
    return query.exec();
}

export { connect, createExercise, getAllExercises, findExerciseById, updateExerciseById, deleteExerciseByFilter};