import random

# une fonction qui génère la grille de terrain
def generate_height_map(size):
    height_map = []
    centers = [
        (size/3, size/3),
        (2*size/3, size/3),
        (size/2, size/2),
        (size/3, 2*size/3),
        (2*size/3, 2*size/3)
    ]  # 5 centres d'iles

    for i in range(size): #haut - bas 
        row = []
        for j in range(size):  # gauche droite 
            height = 0
            for (cx, cy) in centers:
                distance = ((i - cx)**2 + (j - cy)**2)**0.5
                if distance < size/5:
                    local_height = max(0, 20 - (distance * 1.5))

                    # AJOUTER UN VOLCAN SI ON EST PRES DU CENTRE
                    volcano_center = (size/2, size/2)
                    volcano_radius = size/15  # Rayon du volcan (petit cratère)

                    volcano_distance = ((i - volcano_center[0])**2 + (j - volcano_center[1])**2)**0.5

                    if volcano_distance < volcano_radius:
                        # Cratère : forcer la hauteur à être plus basse
                        local_height = max(0, local_height - (volcano_radius - volcano_distance) * 2)
                    
                    # AJOUTER UNE PLAGE
                    if 5 < local_height < 10:
                        local_height = 5  # Hauteur stable pour les plages


                    height = max(height, local_height)

            row.append(height)
        height_map.append(row)
    return height_map


def write_scad(height_map, filename="model.scad"):
    with open(filename, "w") as f:
        f.write("// Generated OpenSCAD model\n")
        f.write("difference() {\n")
        
        # Plaque de l'océan (bleue)
        f.write('  translate([0, 0, 0])\n')
        f.write('     color([0, 0.3, 1])\n')
        f.write(f'        cube([{len(height_map)}, {len(height_map)}, 1], center=false);\n')
        
        # Inscription dessous
        f.write('  translate([60, 3, -0.5])\n')
        f.write('     linear_extrude(height = 1)\n')
        f.write('        mirror([1,0,0])\n')
        f.write('           text("MB- IFT2125-H25", size = 6, font = "Arial", halign = "true");\n')
        f.write('}\n')

        # Terrain (polyhedrons)
        for i in range(len(height_map) - 1):
            for j in range(len(height_map) - 1):
                # Lire la hauteur
                h = height_map[i][j]

                # Définir la couleur selon la hauteur
                if h <= 1:
                    color_r, color_g, color_b = 0, 0.3, 1
                elif h <= 5:
                    color_r, color_g, color_b = 0.96, 0.87, 0.70
                elif h <= 15:
                    color_r, color_g, color_b = 0.3, 0.8, 0.2
                elif h <= 30:
                    color_r, color_g, color_b = 0.1, 0.5, 0.1
                else:
                    color_r, color_g, color_b = 0.8, 0.8, 0.8

                # Ecrire la couleur
                f.write('     color([{},{},{}])\n'.format(color_r, color_g, color_b))

                # Définir les sommets du polyhedron
                p0 = [i, j, height_map[i][j]]
                p1 = [i+1, j, height_map[i+1][j]]
                p2 = [i+1, j+1, height_map[i+1][j+1]]
                p3 = [i, j+1, height_map[i][j+1]]
                p4 = [i, j, 1]
                p5 = [i+1, j, 1]
                p6 = [i+1, j+1, 1]
                p7 = [i, j+1, 1]

                # Ecrire le polyhedron
                f.write('polyhedron(\n')
                f.write('  points = [\n')
                f.write(f'    {p0}, {p1}, {p2}, {p3},\n')
                f.write(f'    {p4}, {p5}, {p6}, {p7}\n')
                f.write('  ],\n')
                f.write('  faces = [\n')
                f.write('    [0, 1, 2, 3],\n')  # dessus
                f.write('    [4, 5, 6, 7],\n')  # dessous
                f.write('    [0, 1, 5, 4],\n')  # côtés
                f.write('    [1, 2, 6, 5],\n')
                f.write('    [2, 3, 7, 6],\n')
                f.write('    [3, 0, 4, 7]\n')
                f.write('  ]\n')
                f.write(');\n')

    with open(filename, "w") as f:
        f.write("// Generated OpenSCAD model\n")
        f.write("difference() {\n")
        # Plaque de l'océan
        f.write('  translate([0, 0, 0])\n')


# <=1	Bleu	Mer
# <=5	Beige	Plage
# <=15	Vert clair	Plaine, herbe
# <=30	Vert foncé	Montagne
# >30	Gris clair/blanc	Sommets

        color_r, color_g, color_b = 0, 0, 0

        h = height_map[i][j]
        if h <= 1:
      # Mer profonde (bleu)
            color_r, color_g, color_b = 0, 0.3, 1
        elif h <= 5:
        # Plage (beige clair)
            color_r, color_g, color_b = 0.96, 0.87, 0.70
        elif h <= 15:
            # Terre (vert clair)
            color_r, color_g, color_b = 0.3, 0.8, 0.2
        elif h <= 30:
            # Montagne (vert foncé)
            color_r, color_g, color_b = 0.1, 0.5, 0.1
        else:
         # Pic montagneux (gris/blanc)
            color_r, color_g, color_b = 0.8, 0.8, 0.8

        f.write('     color([{},{},{}])\n'.format(color_r, color_g, color_b))

        
        
        f.write(f'        cube([{len(height_map)}, {len(height_map)}, 1], center=false);\n')
        # Inscription dessous
        f.write('  translate([60, 3, -0.5])\n')
        f.write('     linear_extrude(height = 1)\n')
        f.write('        mirror([1,0,0])\n')
        f.write('           text("IFT2125-H25", size = 6, font = "Arial", halign = "true");\n')
        f.write('}\n')

        # Terrain (polyhedrons)
        for i in range(len(height_map) - 1):
            for j in range(len(height_map) - 1):
                p0 = [i, j, height_map[i][j]]
                p1 = [i+1, j, height_map[i+1][j]]
                p2 = [i+1, j+1, height_map[i+1][j+1]]
                p3 = [i, j+1, height_map[i][j+1]]
                p4 = [i, j, 1]
                p5 = [i+1, j, 1]
                p6 = [i+1, j+1, 1]
                p7 = [i, j+1, 1]

                f.write('     color([{}, 1, {}])\n'.format(0.1 + height_map[i][j]/40, 0.1 + height_map[i][j]/40))
                f.write('polyhedron(\n')
                f.write('  points = [\n')
                f.write(f'    {p0}, {p1}, {p2}, {p3},\n')
                f.write(f'    {p4}, {p5}, {p6}, {p7}\n')
                f.write('  ],\n')
                f.write('  faces = [\n')
                f.write('    [0, 1, 2, 3],\n')
                f.write('    [4, 5, 6, 7],\n')
                f.write('    [0, 1, 5, 4],\n')
                f.write('    [1, 2, 6, 5],\n')
                f.write('    [2, 3, 7, 6],\n')
                f.write('    [3, 0, 4, 7]\n')
                f.write('  ]\n')
                f.write(');\n')

def main():
    size = 50  # Taille de la grille (50x50)
    height_map = generate_height_map(size)
    write_scad(height_map)

if __name__ == "__main__":
    main()
