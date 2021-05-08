x = np.array([20,100,1400,1500,2000,5000,10000,20000,30000,65000])
proper = np.array([0.557, 0.592, 0.565, 0.759, 0.782, 1.082, 1.167, 1.628, 2.086, 3.647])
intermedi = np.array([4.927, 4.710, 4.851, 5.388, 5.588, 6.567, 7.961, 8.535, 9.344, 0])
llunya = np.array([136.25,136.221,136.556,136.58,136.49,137.978,139.092,139.543,140.379,142.406])

plt.figure(figsize=(15, 10),dpi=600)

plt.plot(x.astype('str'),proper,'g^--' ,label='Proper') #g.-- == color, marker,tipo de linia.
plt.plot(x[:9].astype('str'),intermedi[:9],'c*--' ,label='Intermedi')
plt.plot(x.astype('str'),llunya,'r.--' ,label='Llunya')

plt.title('Retard dels nodes', fontdict={'fontname':'Times New Roman', 'fontsize': 20})
plt.xlabel('bytes')
plt.ylabel('ms')

plt.yticks(np.arange(0, 160, step=10))
plt.legend()
plt.show()