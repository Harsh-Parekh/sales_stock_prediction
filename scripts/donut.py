import matplotlib.pyplot as plt


def make_donut_chart(dict):
    labels = ['Fivestar', 'Fourstar', 'Threestar', 'Twostar', 'Onestar']
    sizes = [dict['fivepercentage'], dict['fourpercentage'], dict['threepercentage'], dict['twopercentage'],
             dict['onepercentage']]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#68d9df']
    plt.pie(sizes, labels=labels, autopct='%1.0f%%', shadow=False, startangle=90, colors=colors, radius=0.85,
            pctdistance=0.75)
    circle = plt.Circle((0, 0), 0.5, color='black', fc='white', linewidth=0)
    donut = plt.gcf()
    donut.gca().add_artist(circle)
    donut.set_size_inches(4, 4)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('/home/spy/projectworkspace/salesstockprediction/base/static/adminResources/image/plot')
    plt.close()
