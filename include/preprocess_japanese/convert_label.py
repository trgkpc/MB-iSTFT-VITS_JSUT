""" from https://github.com/Wataru-Nakata/FastSpeech2-JSUT """

import re
import os
import sys

class ExtentionException(Exception):
    pass

class EmptyLabelException(Exception):
    pass


class Segment:
    """
    a unit of speech (i.e. phoneme, mora)
    """
    def __init__(self, tStart, tEnd, label):
        self.tStart = tStart
        self.tEnd = tEnd
        self.label = label

    def __add__(self, other):
        return Segment(self.tStart, other.tEnd, self.label + other.label)

    def can_follow(self, other):
        """
        return True if Segment self can follow Segment other in one mora,
        otherwise return False
        example: (other, self)
             True: ('s', 'a'), ('sh', 'i'), ('ky', 'o:'), ('t', 's')
             False: ('a', 'q'), ('a', 's'), ('u', 'e'), ('s', 'ha')
        """
        vowels = ['a', 'i', 'u', 'e', 'o', 'a:', 'i:', 'u:', 'e:', 'o:']
        consonants = ['w', 'r', 't', 'y', 'p', 's', 'd', 'f', 'g', 'h', 'j',
                      'k', 'z', 'c', 'b', 'n', 'm']
        only_consonants = lambda x: all([c in consonants for c in x])
        if only_consonants(other.label) and self.label in vowels:
            return True
        if only_consonants(other.label) and only_consonants(self.label):
            return True
        return False

    def to_textgrid_lines(self, segmentIndex):
        label = '' if self.label in ['silB', 'silE'] else self.label
        return [f'        intervals [{segmentIndex}]:',
                f'            xmin = {self.tStart} ',
                f'            xmax = {self.tEnd} ',
                f'            text = "{label}" ']



def openjtalk2julius(p3):
    if p3 in ['A','I','U',"E", "O"]:
        return p3.lower()
    if p3 == 'cl':
        return 'q'
    if p3 == 'pau':
        return 'sp'
    return p3
    
def read_lab(filename):
    """
    read label file (.lab) generated by Julius segmentation kit and 
    return SegmentationLabel object
    """
    try:
        if not re.search(r'\.lab$', filename):
            raise ExtentionException("read_lab supports only .lab")
    except ExtentionException as e:
        print(e)
        return None
        
    with open(filename, 'r') as f:
        labeldata = [line.split() for line in f if line != '']
        segments = [Segment(tStart=float(line[0])/10e6, tEnd=float(line[1])/10e6, 
                            label=openjtalk2julius(re.search(r"\-(.*?)\+", line[2]).group(1))) for line in labeldata]
        return SegmentationLabel(segments)


class SegmentationLabel:
    """
    list of segments
    """
    def __init__(self, segments, separatedByMora=False):
        self.segments = segments
        self.separatedByMora = separatedByMora

    def by_moras(self):
        """
        return new SegmentationLabel object whose segment are moras 
        """
        if self.separatedByMora == True:
            return self

        moraSegments = []
        curMoraSegment = None
        for segment in self.segments:
            if curMoraSegment is None:
                curMoraSegment = segment
            elif segment.can_follow(curMoraSegment):
                curMoraSegment += segment
            else:
                moraSegments.append(curMoraSegment)
                curMoraSegment = segment
        if curMoraSegment:
            moraSegments.append(curMoraSegment)
        return SegmentationLabel(moraSegments, separatedByMora=True)

    def _textgrid_headers(self):
        segmentKind = 'mora' if self.separatedByMora else 'phones'
        return ['File type = "ooTextFile"',
                'Object class = "TextGrid"',
                ' ',
                'xmin = 0 ',
               f'xmax = {self.segments[-1].tEnd} ',
                'tiers? <exists> ',
                'size = 1 ',
                'item []: ',
                '    item [1]: ',
                '        class = "IntervalTier" ',
               f'        name = "{segmentKind}" ',
                '        xmin = 0 ',
               f'        xmax = {self.segments[-1].tEnd} ',
               f'        intervals: size = {len(self.segments)} ']

    def to_textgrid(self, textgridFileName):
        """
        save to .TextGrid file, which is available for Praat
        """
        try:
            if not self.segments:
                raise EmptyLabelException(f'warning: no label data found in '
                                          f'{textgridFileName}')
        except EmptyLabelException as e:
            print(e)
            return

        textgridLines = self._textgrid_headers()
        for i, segment in enumerate(self.segments):
            textgridLines.extend(segment.to_textgrid_lines(i + 1))
        with open(textgridFileName, 'w') as f:
            f.write('\n'.join(textgridLines))


if __name__ == '__main__':
    args = sys.argv
    if len(args) >= 2:
        mainDirectory = args[1]
    else:
        mainDirectory = os.curdir

    answer = None
    while not answer in ['y', 'Y', 'n', 'N']:
        answer = input('change segmentation unit to mora?'\
                       ' (default:phoneme) y/n:')
        choosesMora = answer in ['y', 'Y']

    for dirPath, dirNames, fileNames in os.walk(mainDirectory):
        labFileNames = [n for n in fileNames if re.search(r'\.lab$', n)]

        for labFileName in labFileNames:
            label = read_lab(os.path.join(dirPath, labFileName))
            if choosesMora:
                label = label.by_moras()
            textgridFileName = re.sub(r"\.lab$", ".TextGrid", labFileName)
            label.to_textgrid(os.path.join(dirPath, textgridFileName))