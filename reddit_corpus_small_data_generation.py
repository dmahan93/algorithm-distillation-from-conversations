from collections import defaultdict
from convokit import Corpus, download, Conversation
import random
from datasets import Dataset
import tqdm


def grab_convo_dict_and_top_level(conv: Conversation):
    convo_dict = defaultdict(list)
    text = conv.meta['title']
    next_selections = list()
    select_id = None
    for utt in conv.iter_utterances():
        if utt.reply_to is not None:
            convo_dict[utt.reply_to].append(utt)
        elif utt.meta['top_level_comment'] is None:
            text = utt.speaker.name + '\n' + text + '\n' + utt.text
            select_id = utt.id
    text = text + "<BACKGROUND_INDEX_TOKEN>"
    return select_id, convo_dict, text


def random_walk(conv: Conversation):
    select_id, convo_dict, text = grab_convo_dict_and_top_level(conv)
    # Sort by score, higher scores should have preference over smaller scores.
    # Why for random walk? My intuition tells me the highest score is likely to be the median preference, and it
    # diverges from there.
    next_selections = sorted(convo_dict[select_id], key=lambda x:x.meta['score'], reverse=True)
    # Guard against bad data
    if next_selections == []:
        return None
    while next_selections is not None:
        for i, select in enumerate(next_selections):
            # If it's the only utterance, we have to use it
            if i == len(next_selections)-1:
                text += select.speaker.name + '\n' + select.text + "<SELECTED_UTTERANCE>"
                next_selections = convo_dict[select.id]
                if len(next_selections) == 0:
                    next_selections = None
                break
            else:
                # Randomly sample conversation branches
                if random.randint(0, 1) == 1:
                    # Reject this branch
                    text += select.speaker.name + '\n' + select.text + "<REJECTED_UTTERANCE>"
                    continue
                else:
                    # Select this branch
                    text += select.speaker.name + '\n' + select.text + "<SELECTED_UTTERANCE>"
                    next_selections = convo_dict[select.id]
                    if len(next_selections) == 0:
                        next_selections = None
                    break
    return text


def top_two(conv: Conversation):
    select_id, convo_dict, text = grab_convo_dict_and_top_level(conv)
    next_selections = sorted(convo_dict[select_id], key=lambda x:x.meta['score'], reverse=True)
    # Guard against bad data
    if next_selections == []:
        return None
    while next_selections is not None:
        # add in some random sampling, no need to ensure it ALWAYS does top 2 on the outputs right?
        # Also check if it's not just a single utterance in the selections
        if (len(next_selections) > 1) and (random.randint(0, 2) < 2):
            text += next_selections[1].speaker.name + '\n' + next_selections[1].text + "<REJECTED_UTTERANCE>"
            text += next_selections[0].speaker.name + '\n' + next_selections[0].text + "<SELECTED_UTTERANCE>"
        else:
            text += next_selections[0].speaker.name + '\n' + next_selections[0].text + "<SELECTED_UTTERANCE>"
        next_selections = convo_dict[next_selections[0].id]
        if len(next_selections) == 0:
            next_selections = None
    return text


if __name__ == '__main__':
    corpus = Corpus(download("reddit-corpus-small"))
    rw_texts = []
    t2_texts = []
    for key, convo in tqdm.tqdm(corpus.conversations.items()):
        rw_texts.append(random_walk(convo))
        t2_texts.append(top_two(convo))
    Dataset.from_dict({"text": rw_texts}).push_to_hub("dmayhem93/random-walk-reddit-corpus-small")
    Dataset.from_dict({"text": t2_texts}).push_to_hub("dmayhem93/top-2-reddit-corpus-small")