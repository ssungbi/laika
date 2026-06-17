import codecs

html = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()

old_containers = """                    <!-- Explanations Container -->
                    <div id="disability-explanations" class="explanations-group hidden">
                        <!-- JS will populate this -->
                    </div>"""

new_containers = """                    <!-- Explanations Container -->
                    <div id="disability-explanations" class="explanations-group hidden">
                        <!-- JS will populate this -->
                    </div>
                    <!-- Chongchik Container (v0505) -->
                    <div id="disability-chongchik" class="explanations-group hidden">
                        <!-- JS will populate this -->
                    </div>
                    <!-- Criteria Container (v0505) -->
                    <div id="disability-criteria" class="explanations-group hidden">
                        <!-- JS will populate this -->
                    </div>"""

html = html.replace(old_containers, new_containers)

codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(html)
print("index.html updated.")
