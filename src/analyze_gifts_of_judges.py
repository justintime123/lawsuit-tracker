#https://www.courtlistener.com/help/api/rest/financial-disclosures/

#Current Supreme Court justices
#https://www.supremecourt.gov/about/biographies.aspx
scotus_judges = ['John Glover Roberts', 'Clarence Thomas', 'Samuel Anthony Alito', 'Sonia Sotomayor',
                 'Elena Kagan', 'Neil McGill Gorsuch', 'Brett Michael Kavanaugh', 'Amy Coney Barrett',
                 'Ketanji Brown Jackson']

if __name__=='__main__':
    #Get ids of judges
    for judge in scotus_judges:
        name = scotus_judges.split(" ")