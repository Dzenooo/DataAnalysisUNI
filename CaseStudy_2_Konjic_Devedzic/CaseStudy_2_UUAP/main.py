import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/smmh.csv")

df.columns = [
    'timestamp', 'age', 'gender', 'relationship_status', 'occupation',
    'organization', 'uses_social_media', 'platforms', 'screen_time',
    'purposeless_use', 'distracted_by_sm', 'restless_without_sm',
    'easily_distracted', 'bothered_by_worries', 'concentration_issues',
    'compare_to_others', 'feel_about_comparisons', 'seek_validation',
    'feel_depressed', 'interest_fluctuation', 'sleep_issues'
]

df = df[df['uses_social_media'] == 'Yes']
df = df[df['age'].between(13, 35)]
df['gender'] = df['gender'].apply(
    lambda x: 'Ostalo' if x not in ['Male', 'Female'] else x
)

screen_time_order = [
    'Less than an Hour', 'Between 1 and 2 hours', 'Between 2 and 3 hours',
    'Between 3 and 4 hours', 'Between 4 and 5 hours', 'More than 5 hours'
]
screen_time_labels = ['Manje od 1h', '1-2h', '2-3h', '3-4h', '4-5h', 'Više od 5h']

df['screen_time'] = pd.Categorical(df['screen_time'], categories=screen_time_order, ordered=True)

print(f"Učitano {len(df)} ispitanika nakon čišćenja")

#users-screen time plot
screen_counts = df['screen_time'].value_counts().reindex(screen_time_order)

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=screen_time_labels, y=screen_counts.values,
                 hue=screen_time_labels, palette='Blues_d', legend=False)
plt.title('Raspodjela ispitanika po dnevnom vremenu na društvenim mrežama')
plt.xlabel('Dnevno vrijeme na društvenim mrežama')
plt.ylabel('Broj ispitanika')
for idx, value in enumerate(screen_counts.values):
    ax.text(idx, value + 0.5, str(value), ha='center', va='bottom')
plt.tight_layout()
plt.savefig('graf1_screentime.png', dpi=300, bbox_inches='tight')
plt.show()

#depresija i screen time
prosjek_depresija = df.groupby('screen_time', observed=True)['feel_depressed'].mean().reindex(screen_time_order)

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=screen_time_labels, y=prosjek_depresija.values,
                 hue=screen_time_labels, palette='Reds_d', legend=False)
plt.title('Prosječni nivo depresije po dnevnom screen timeu')
plt.xlabel('Dnevno vrijeme na društvenim mrežama')
plt.ylabel('Prosječni nivo depresije (1-5)')
plt.ylim(0, 5)
for idx, value in enumerate(prosjek_depresija.values):
    ax.text(idx, value + 0.05, f'{value:.2f}', ha='center', va='bottom')
plt.tight_layout()
plt.savefig('graf2_depression.png', dpi=300, bbox_inches='tight')
plt.show()

#distrakcija i ovisnost po spolu
df_gender = df[df['gender'].isin(['Male', 'Female'])]

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
for ax, col, title, ylabel in zip(
    axes,
    ['easily_distracted', 'restless_without_sm'],
    ['Nivo distrakcije po spolu', 'Ovisnost o društvenim mrežama po spolu'],
    ['Nivo distrakcije (1-5)', 'Nivo nemira (1-5)']
):
    sns.boxplot(data=df_gender, x='gender', y=col,
                hue='gender', palette='Set2', ax=ax, legend=False)
    ax.set_title(title)
    ax.set_xlabel('Spol')
    ax.set_ylabel(ylabel)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Ženski', 'Muški'])
plt.tight_layout()
plt.savefig('graf3_distraction_addiction.png', dpi=300, bbox_inches='tight')
plt.show()

#heatmap korelacije
numeric_cols = ['purposeless_use', 'distracted_by_sm', 'restless_without_sm',
                'easily_distracted', 'bothered_by_worries', 'concentration_issues',
                'compare_to_others', 'seek_validation', 'feel_depressed',
                'interest_fluctuation', 'sleep_issues']
labels = ['Bespotrebno korištenje', 'Distrakcija', 'Ovisnost o društvenim mrežama',
          'Laka distrakcija', 'Uznemirenost', 'Problemi koncentracije',
          'Poređenje s drugima', 'Traženje validacije', 'Depresija',
          'Fluktuacija interesa', 'Problemi sa snom']

plt.figure(figsize=(12, 10))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f',
            vmin=-1, vmax=1, linewidths=0.5, xticklabels=labels, yticklabels=labels)
plt.title('Korelacija između varijabli mentalnog zdravlja')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('graf4_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

#briga u odnosu na status veze
status_order = ['Single', 'In a relationship', 'Married', 'Divorced']
status_labels = ['Samac', 'U vezi', 'Oženjen/Udata', 'Razveden/a']

prosjek_status = df.groupby('relationship_status')['bothered_by_worries'].mean().reindex(status_order)

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=status_labels, y=prosjek_status.values,
                 hue=status_labels, palette='Purples_d', legend=False)
plt.title('Prosječni nivo briga po statusu veze')
plt.xlabel('Status veze')
plt.ylabel('Prosječna vrijednost (1-5)')
plt.ylim(0, 5)
for idx, value in enumerate(prosjek_status.values):
    ax.text(idx, value + 0.05, f'{value:.2f}', ha='center', va='bottom')
plt.tight_layout()
plt.savefig('graf5_relationship.png', dpi=300, bbox_inches='tight')
plt.show()

#screen time po zanimanju
occupation_order = ['School Student', 'University Student', 'Salaried Worker']
occupation_labels = ['Učenik', 'Student', 'Zaposleni']

df_occ = df[df['occupation'].isin(occupation_order)].copy()
screen_time_num = {
    'Less than an Hour': 0.5, 'Between 1 and 2 hours': 1.5,
    'Between 2 and 3 hours': 2.5, 'Between 3 and 4 hours': 3.5,
    'Between 4 and 5 hours': 4.5, 'More than 5 hours': 6.0
}
df_occ['screen_time_num'] = df_occ['screen_time'].astype(str).map(screen_time_num)
prosjek_occ = df_occ.groupby('occupation')['screen_time_num'].mean().reindex(occupation_order)

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=occupation_labels, y=prosjek_occ.values,
                 hue=occupation_labels, palette='Oranges_d', legend=False)
plt.title('Prosječni dnevni screen time po zanimanju')
plt.xlabel('Zanimanje')
plt.ylabel('Prosječni sati na društvenim mrežama')
plt.ylim(0, 7)
for idx, value in enumerate(prosjek_occ.values):
    ax.text(idx, value + 0.05, f'{value:.2f}h', ha='center', va='bottom')
plt.tight_layout()
plt.savefig('graf6_occupation_screentime.png', dpi=300, bbox_inches='tight')
plt.show()

#problemi sa snom u odnosu na screen time
prosjek_san = df.groupby('screen_time', observed=True)['sleep_issues'].mean().reindex(screen_time_order)

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=screen_time_labels, y=prosjek_san.values,
                 hue=screen_time_labels, palette='Blues_d', legend=False)
plt.title('Prosječni nivo problema sa snom po dnevnom screen timeu')
plt.xlabel('Dnevno vrijeme na društvenim mrežama')
plt.ylabel('Prosječni nivo problema sa snom (1-5)')
plt.ylim(0, 5)
for idx, value in enumerate(prosjek_san.values):
    ax.text(idx, value + 0.05, f'{value:.2f}', ha='center', va='bottom')
plt.tight_layout()
plt.savefig('graf7_sleep_screentime.png', dpi=300, bbox_inches='tight')
plt.show()

#poređenje s drugima i validacija u odnosu na screen time
prosjek_gender = df_gender.groupby('gender')[['compare_to_others', 'seek_validation']].mean()

x = range(2)
width = 0.35

plt.figure(figsize=(10, 6))
bars1 = plt.bar([i - width/2 for i in x],
                [prosjek_gender.loc['Female', 'compare_to_others'],
                 prosjek_gender.loc['Male', 'compare_to_others']],
                width, label='Poređenje sa drugima', color='#9b59b6', alpha=0.8)
bars2 = plt.bar([i + width/2 for i in x],
                [prosjek_gender.loc['Female', 'seek_validation'],
                 prosjek_gender.loc['Male', 'seek_validation']],
                width, label='Traženje validacije', color='#e67e22', alpha=0.8)
plt.title('Poređenje s drugima i traženje validacije po spolu')
plt.xlabel('Spol')
plt.ylabel('Prosječna vrijednost (1-5)')
plt.xticks(x, ['Ženski', 'Muški'])
plt.legend()
plt.ylim(0, 5)
for bar in bars1:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{bar.get_height():.2f}', ha='center', va='bottom')
for bar in bars2:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{bar.get_height():.2f}', ha='center', va='bottom')
plt.tight_layout()
plt.savefig('graf8_validation.png', dpi=300, bbox_inches='tight')
plt.show()