# cs454-resilience
- that other repo fucking stinks, so we have decided to abandon it
- we found an experiment by microsoft that was benchmarking different model's ability to generate text descriptions of input code (which should sound familiar :))

# NEW PLAN:
- we make a similar benchmark, what we benchmark is "how resilient are these models to metamorphic transformations?"
- how? first we need a dataset of python code with text descriptions
- Then, for the model we are testing, we create a second version of the dataset, replacing the original code with the result of our GA for metamorphic transformations
- We can then run the benchmark on the original dataset and our transformed dataset, WE EXPECT that the score for the transformed dataset will be worse, and the difference between these two scores will be our measure of resilience
- LOWER SCORE = MORE RESILIENT MODEL
- We repeat this for several different models in the final report, but for wednesday lets focus on CodeBERT.

[HERE IS THE EXPERIMENT](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Text/code-to-text)

## GA
- The GA is almost the same as before, for some model and input program, we want to find the metamorphic transformation on that program that is as "different" as possible to the model
- this "difference" is our fitness function
  - we can use the metric they use in the experiment, bleu-4 score
  - therefore, the function (as in the python function) for our function needs to be something that can take a model and an expected description as an input, then the output is this bleu-4 score (see [here](https://github.com/microsoft/CodeXGLUE/blob/main/Code-Text/code-to-text/code/bleu.py)).
- mutation is fathony's job, same as before (ty fathony :) )


## THE MODEL
- The CodeBert model which the experient uses in their examples is actually just an encoder model, there is a training script that they run to create a generation model out of it.
- So I guess a high priority is to run this script and get us a working CodeBert generation model


## PRIORITIES (deadline, end of tuesday?)
- GET US A TRAINED MODEL (perhaps a big task)
- WRITE THE SKELETON OF GA (done? needs testing once everything else is added)
- PREPARE A THE DATASET (shouldnt be that big a task)
- GET US SOME MUTATION OPERATORS
- GET US A FITNESS FUNCTION
