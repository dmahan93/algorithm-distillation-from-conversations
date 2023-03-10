# algorithm-distillation-from-conversations
Algorithm Distillation + Pretraining Language Models with Human Preferences + Chat

## Models

Two models are available based on the below datasets:

[Top 2 v0](https://huggingface.co/dmayhem93/Top2ADC_v0), [Random Walk v0](https://huggingface.co/dmayhem93/RandomWalkADC_v0)

Top 2 seems to start grokking removing bad continuations, and random walk just feels fun to use.

Not sure if not enough training or leakage due to seeing other posts, but it sometimes just expands on the previous
thread when it samples/manually add in a \<REJECTED_UTTERANCE>, will need to add in more data for the next run to see.

## Datasets

Two datasets available, based on [reddit corpus small](https://convokit.cornell.edu/documentation/reddit-small.html)

### [top-2-reddit-corpus-small](https://huggingface.co/datasets/dmayhem93/top-2-reddit-corpus-small)

This dataset uses reddit scores to rank the different conversation replies to the current reply.

It then takes the top 2 of these and does second_place_text\<REJECTED_UTTERANCE>first_place_text\<SELECTED_UTTERANCE>.

If there's only one, or on a random chance, we just use the first place text.

This continues until the conversation thread has no more replies to it.
  
The goal (hopefully) is to learn to use rejected text and improve on it.
 
### [random-walk-reddit-corpus-small](dmayhem93/random-walk-reddit-corpus-small)

This dataset uses reddit scores to rank the different conversation replies to the current reply.

We then do a coinflip, if 0, we add text\<REJECTED_UTTERANCE> and go the next reply.

If 1, or the last one, we add text\<SELECTED_UTTERANCE>.

This continues until the conversation thread has no more replies to it.
  
The goal (hopefully) is to learn to use rejected text as negative preferences on the direction the text should go.
 


## Citations
```bibtex
@misc{https://doi.org/10.48550/arxiv.2210.14215,
  doi = {10.48550/ARXIV.2210.14215},
  
  url = {https://arxiv.org/abs/2210.14215},
  
  author = {Laskin, Michael and Wang, Luyu and Oh, Junhyuk and Parisotto, Emilio and Spencer, Stephen and Steigerwald, Richie and Strouse, DJ and Hansen, Steven and Filos, Angelos and Brooks, Ethan and Gazeau, Maxime and Sahni, Himanshu and Singh, Satinder and Mnih, Volodymyr},
  
  keywords = {Machine Learning (cs.LG), Artificial Intelligence (cs.AI), FOS: Computer and information sciences, FOS: Computer and information sciences},
  
  title = {In-context Reinforcement Learning with Algorithm Distillation},
  
  publisher = {arXiv},
  
  year = {2022},
  
  copyright = {Creative Commons Attribution 4.0 International}
}
@misc{https://doi.org/10.48550/arxiv.2302.08582,
  doi = {10.48550/ARXIV.2302.08582},
  
  url = {https://arxiv.org/abs/2302.08582},
  
  author = {Korbak, Tomasz and Shi, Kejian and Chen, Angelica and Bhalerao, Rasika and Buckley, Christopher L. and Phang, Jason and Bowman, Samuel R. and Perez, Ethan},
  
  keywords = {Computation and Language (cs.CL), Machine Learning (cs.LG), FOS: Computer and information sciences, FOS: Computer and information sciences},
  
  title = {Pretraining Language Models with Human Preferences},
  
  publisher = {arXiv},
  
  year = {2023},
  
  copyright = {Creative Commons Attribution 4.0 International}
}

```
