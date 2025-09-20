---
permalink: /
title: "About"
excerpt: "About me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

Hi, I am a Ph.D candidate in <a href="https://uilab.kr/">User & Information Lab (U&I Lab)</a>, KAIST. My research interests lie at the intersection of Natural Language Processing and Human-AI Interaction, with a particular focus on English education. I am especially interested in how Large Language Models can be leveraged to enable personalized learning—tailoring educational content to meet the unique needs of individual learners.


Please feel free to contact me via email <code>{firstname}_{lastname} (at) kaist.ac.kr</code>.

## Latest News ([See all](/news))

- 📝 [Sep 2025] Our paper <a href='https://arxiv.org/abs/2505.20875'>Trans-Env</a> is accepted to NeurIPS 2025! 🇺🇲 
- 📝 [May 2025] Our paper <a href='https://aclanthology.org/2025.acl-long.659/'>DREsS</a> is accepted to ACL 2025! 👗 
- 👩‍💻 [Mar 2025] I will be joining <a href='https://www.microsoft.com/en-us/research/lab/microsoft-research-asia/'> Microsoft Research Asia</a> as an intern starting in this July! 🇨🇳 

## Selected Publications ([See all](/publications))

{% assign publications = site.publications | sort: "selected" %}
{% for post in publications %}
{% if post.selected != "" %}
{% include archive-short-publications.html %}
{% endif %}
{% endfor %}

## Education

- Ph.D. School of Computing, *KAIST*, Feb 2028
  - Advisor: <a href ='https://aliceoh9.github.io/'>Alice Oh</a>, <a href='https://sites.google.com/view/soyeonahn/about'>So-Yeon Ahn</a>
- M.S. School of Computing, *KAIST*, Feb 2024
  - Advisor: <a href='https://sites.google.com/view/soyeonahn/about'>So-Yeon Ahn</a>, <a href ='https://aliceoh9.github.io/'>Alice Oh</a>
- B.A. in English Linguistics, B.S. in Software & AI, *HUFS*, Aug 2022
  - Secondary School Teacher License of English

## Academic Services

- Reviewer: NeurIPS ([2024](https://neurips.cc/Conferences/2024/ProgramCommittee)), AIED (2025)
- Organizer: International NLP Workshop at KAIST (2024)

## Teaching Experiences

- TA of AI and Its Social Impact ([Spring 2024](https://uilab-kaist.github.io/coe491-ai-and-society-spring-2024/))
- TA of Public Relation in CS department  (2022-2025)

## Talks & Presentations

{% assign reversed_talks = site.talks | reverse %}
{% for post in reversed_talks limit:7 %}
{% include archive-short-talks.html %}
{% endfor %}

## Honors

- An Outstanding MS Thesis Award, *School of Computing, KAIST*, 2024
- [Government-sponsored Scholarship](https://kaist.ac.kr/), *KAIST*, 2022
- [National Excellence Scholarship](https://www.kosaf.go.kr/ko/main.do), *KOSAF*, 2020
- [Industry-University Research Scholarship](https://www.nia.or.kr/site/nia_kor/main.do), *NIA*, 2020
- [Academic Scholarship](https://www1.kiwoom.com/h/main), *Kiwoom Securities*, 2019

