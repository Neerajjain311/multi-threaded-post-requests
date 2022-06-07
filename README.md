# Multithreaded POST requests using Python

## Task In Hand
Develop system to raise HTTP POST requests with provided Activity Data - to given list of URL endpoints - in parallel and handle errors gracefully.

## Assumptions
1. Auth and other details are provided and need not be worried about while making the POST request.
2. The list of URL endpoints provided are correct, and need no modifications.
3. The data (Activity Data) needs to be validated prior syncing it with other systems - the values shouldn't be empty and must be of specific types.

## Key Learnings
- Revised Logging concepts
- Skimmed through Requests module
- Multithreading - using Thread (i.e. without ThreadPoolExecutor)
- Multithreading using ThreadPoolExecutor
- Revised Python Syntax ;)

## Future Roadmap
- [ ] Validating it on a live endpoint
- [ ] Handle more edge cases - what if the activity id is corrupt? what if the activity is already processed?
- [ ] Study and refine the rate limit exception handling logic


