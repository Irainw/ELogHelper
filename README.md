# ELogHelper

## Motivation
SLAC National Accelerator Lab operators use what is called an E-Log to record their work and keep a log of operations. Oftentimes this serves as a repository for solutions and tracking information about issues that occur in day to day operation. Operators therefore, regularly search the e-log for records of solutions and updating their information about the state of the machine. With the rise of AI, specifically **G**enerative **P**re-trained **T**ransformers (GPTs) and the push to incorporate them more and more into the operation of accelerators I wanted to get ahead of the curve and write my own tool to help automate the searching and interpreting of e-log data. 

ElogHelper is trained on e-log data and the MCCWiki, both datasets are currently private and cannot be accessed outside of the SLAC network, additionally any Personally Identifiable Information, such as names and usernames has been scrubbed from the data prior to training. 