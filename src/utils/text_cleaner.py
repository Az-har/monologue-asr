import re


def remove_repeated_words(text):
    """
    Removes repeated consecutive words.
    Example: 'yes yes yes I think' -> 'yes I think'
    """

    pattern = r'\b(\w+)( \1\b)+'
    return re.sub(pattern, r'\1', text)


def remove_repeated_phrases(text):
    """
    Removes repeated short phrases Whisper sometimes produces.
    """

    words = text.split()
    cleaned = []

    for word in words:

        if len(cleaned) > 3 and word == cleaned[-1]:
            continue

        cleaned.append(word)

    return " ".join(cleaned)


def clean_transcript(text):

    text = remove_repeated_words(text)
    text = remove_repeated_phrases(text)

    # fix spacing
    text = re.sub(r'\s+', ' ', text)

    return text.strip()