To run tests in the docker on your localhost:
1. Download Python image:
 
      ```docker pull python```
 
2. Build docker image:

      ```docker build -t pytest_runner . ```
  
3. Run tests in docker:

      ```docker run --rm --mount type=bind,src=/path/to/tests,dst=/open_brewery_project/ pytest_runner```
