# Agean Engine 
This is the engine built with the event pipeline that is going to be used by the browser extension and the server. 


#TODO: write the documentation for the engine well and remove all the fluff that isn't supposed to be here. the testing files and then the parts of the pipeline that aren't in use. might be useful to have some kind of archives file that contains those things after I've gathered that data I need for testing purposes.

## Fixes
- [ ] what happens if no code is found in the frame(stop the pipeline)
- [ ] there could be a bug where when the pipeline is running in async mode, and then there is a file that is downloaded, and then 
two people are trying to extract code from the same file, one of the procsessing would be more forward than the other.
