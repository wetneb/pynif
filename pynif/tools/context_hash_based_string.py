import hashlib
import urllib

def context_hash_based_string(text: str, original_uri: str, beginIndex: int = None, length: int = None, endIndex: int = None, context_length: int = 10, safe: bool = False) -> str:
        """
        ContextHashBasedString algorithm adapted from
        the paper Linked-Data Aware URI Schemes for Referencing Text Fragments
        (https://doi.org/10.1007/978-3-642-33876-2_17) page 4.
        """
        if len(text) <= 0:
            raise TypeError("Empty string. The length of the argument 'text' must be > 0")
        if beginIndex is None:  # Hash full text
            beginIndex = 0
            endIndex = len(text)
        elif length is not None:  # beginIndex and length are provided
            endIndex = beginIndex + length
        elif endIndex is None:  # beginIndex and endIndex are provided
            raise TypeError("At least one argument 'length' or 'endIndex' must be provided")
        
        scheme_identifier = '#hash'
        context_string = text[beginIndex:endIndex]
        overall_length = len(context_string)

        #Adjust the beging and end indexes to temove the white space before and after the annotated string
        for char in context_string:
            if char == " ":
                beginIndex = beginIndex + 1
            else:
                break
        for char in reversed(context_string):
            if char == " ":
                endIndex = endIndex - 1
            else:
                break
        
        # String = the annotated string
        adjusted_string = text[beginIndex:endIndex]

        # leftContext_length, rightContext_length are the context length around the string to be annotated
        leftContext_length = context_length
        rightContext_length = context_length

        # Adjust the leftContext_length and rightContext_length so it does not overflow the text
        if beginIndex - context_length < 0:
            leftContext_length = beginIndex
        if endIndex + context_length > len(text):
            rightContext_length = len(text) - endIndex
        
        # Updating the the value context_length no the max value
        context_length = max(leftContext_length, rightContext_length)

        # message_digest_string = context_before_string + (adjusted_string) + context_after_string
        message_digest_string = text[(beginIndex-leftContext_length):beginIndex] \
                                + '('+adjusted_string+')'\
                                + text[endIndex:(endIndex+rightContext_length)]

        message_digest = hashlib.md5(message_digest_string.encode('utf-8')).hexdigest()

        string = urllib.parse.quote(context_string[0:20], safe='') #First 20 characters of the full context

        contextHashBasedString = original_uri.split('#')[0] + scheme_identifier + '_' + str(context_length) + '_' + str(overall_length) + '_' + message_digest + '_' + string
        
        # Extended version of ContextHashBasedString:
        # add the beginIndex and endIndex of the phrase to the generated URI
        # to further guaranty its uniqueness
        # -
        # It is also possible to extend the context_length but not work in every case
        if safe:
            contextHashBasedString += '_' + str(beginIndex) + '_' + str(endIndex)
        return contextHashBasedString