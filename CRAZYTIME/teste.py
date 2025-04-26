#historico = browser.find_elements_by_xpath('//*[@class="itemsContainer--525e7 fadeElements--c299a"]')

#contador = 0

for a in aaa:
    if not contador == 7:
        if a.text == '':
           bbb.append('bonus')
           contador+=1
        else:   
           bbb.append(a.text)
           contador+=1
           continue
    else:
        contador = 0