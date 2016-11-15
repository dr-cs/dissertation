set   autoscale              # scale axes automatically
unset log                    # remove anylog-scaling
unset label                  # remove any previous labels
set xtic auto                # set xtics automatically
set ytic auto                # set ytics automatically
set title 'Bunny Wolf'
set xlabel 'Trials x 5000'
set ylabel 'Average Score per Time Step'
set key bottom right
set term png enh
set out 'bunny-wolf.png'

plot "bunny-wolf-1.dat" using 1:2 title 'Arbi-Q with Incomprable Rewards' with linespoints, \
     "bunny-wolf-2.dat" using 1:2 title 'Arbi-Q' with linespoints