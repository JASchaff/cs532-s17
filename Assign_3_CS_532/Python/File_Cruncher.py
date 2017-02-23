from sys import argv
import bs4
import  os

class file_cruncher():
    #checks visibility of element
    def visible(self, element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'meta']:
            return False
        elif isinstance(element, bs4.element.Comment):
            return False
        return True
    #converts html file to txt file of visible text
    def de_HTML(self, filepath):
        soup=bs4.BeautifulSoup(open(filepath),'html.parser')
        texts=soup.find_all(text=True)
        visible_text=filter(self.visible, texts)
        newfilepath=os.path.join(os.path.dirname(filepath), (os.path.splitext(os.path.basename(filepath))[0].rstrip() + '.txt'))
        outfile=open(newfilepath, 'w')
        outfile.writelines('%s\n' % line for line in visible_text)
        outfile.close()
        
if __name__ == '__main__':
    directory=argv[1]
    fc=file_cruncher()
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            filepath=os.path.join(directory, filename)
            fc.de_HTML(filepath)
            print('Converted: ' + filepath +'\n')
    
