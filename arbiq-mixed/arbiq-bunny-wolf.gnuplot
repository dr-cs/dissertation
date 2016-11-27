set   autoscale              # scale axes automatically
unset log                    # remove anylog-scaling
unset label                  # remove any previous labels
set xtic auto                # set xtics automatically
set ytic auto                # set ytics automatically
set title 'Arbi-Q on the Bunny Wolf Problem with Various combinations of Q-Learning and Sarsa Modules, Comparable and Incomparable Rewards'
set xlabel 'Time Steps x 1000'
set ylabel 'Average Score per Time Step'
set key bottom right
set term png enh
set out 'arbiq-bunny-wolf.png'

plot "arbiq-bunny-wolf-1.dat" using 1:2 title 'Arbi-Q, Sarsa and Q-Learning Modules' with linespoints, \
     "arbiq-bunny-wolf-2.dat" using 1:2 title 'Arbi-Q, Sarsa modules with Incomprable Rewards' with linespoints, \
     "arbiq-bunny-wolf-3.dat" using 1:2 title 'Arbi-Q, Sarsa modules' with linespoints