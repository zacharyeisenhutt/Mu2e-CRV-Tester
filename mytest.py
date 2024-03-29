x=0
while x==0:
	namelist=[br'1.2v_Pos *',br'1.8v_Pos *',br'5.0v_Pos',br'10v_Pos',br'2.5v_Pos',br'5.0v_Neg',br'15v_Pos',br'3.3v_Pos']
	evlist=[1.2,1.8,5.0,10,2.5,5.0,15,3.3]
	for i in range(len(evlist)):
		s.expect(namelist[i])
		s.expect(b'-*[0-9.]+')
		v = float(s.match.group(0))
		ev=evlist[1]
		e=((ev-v)/ev)*100
		assert abs(e)< 10
		print(" **** This is the expected voltage", ev,"," " This is the actual voltage", v, "," "This is the error", e, "% !!!!")
s.data.clear()
y = 1
biaslist = [br'Bias_0',br'Bias_1',br'Bias_2',br'Bias_3',br'Bias_4',br'Bias_5',br'Bias_6',br'Bias_7']
while y==1:
	for i in range(len(biaslist)):
		s.expect(biaslist[i])
		s.expect(b'-*[0-9.]+')
		bv = float(s.match.group(0))
		assert bv<1
		print(" **** Tbe bias volatge is", bv, " !!!!")
s.data.clear()
s.expect(br'Temp_C.*\n')
s.expect(b'-*[0-9.]+')
temp=float(s.match.group(0))
assert 18<temp<30
print(" **** The temperature is", temp, "degC !!!!")
s.data.clear()	

if 69>=addr>=48:
			dac=addr-48
			fpga=0
			print("**** Your FPGA and DAC are", fpga,",", dac," !!!!")
		if 1093>=addr>=1072:
			dac=addr-1072
			fpga=1
			print("**** Your FPGA and DAC are", fpga,",", dac," !!!!")
		if 2117>=addr>=2096:
			dac=addr-2096
			fpga=2
			print("**** Your FPGA and DAC are", fpga,",", dac," !!!!")
		if 3141>=addr>=3120:
			dac=addr-3120
			fpga=3
			print("**** Your FPGA and DAC are", fpga,",", dac," !!!!")	

csv_catcher=[]	
def plot_histo(all_histos):
    #Code error specifices that all_histos is not defined, should I make it a global variable.
    intTime_ms=10
    #all_histos = takeAndReadAll64(s, intTime_ms)
    x=np.arange(0,N_HISTO_BINS)
    figure, axes = plt.subplots(8, 8, sharex=True, sharey=True)
    axes = axes.flatten()
    for ich in range(0,N_SIPM):
        y=np.array(all_histos[ich, :])
        a,b =np.polyfit(x, y, 1)
        if ich == 59:
            axes[ich].set_xlabel('Bin #')
        if ich == 24:
            axes[ich].set_ylabel('# of Counts')
        if ich == 3:
            axes[ich].set_title('# of Counts vs. Bin #')
        axes[ich].scatter(x,y)
        ymax = max(y)
        axes[ich].text(N_HISTO_BINS//2, ymax-1, "max %d" % ymax, va="top", ha="center")
        header=['Bset_in #','# of Counts']
        with open(f'Data/plot_histo{ich}_{time.strftime("%Y-%m-%d_%H-%M-%S")}.csv', 'w', encoding='UTF8', newline='') as f:
            writer=csv.writer(f)
            writer.writerow(header)
            for i in range(len(x)):
                writer.writerow([x[i], y[i]])
            csv_catcher.append(f)
    plt.show()

def analyse_histo(s):
    intTime_ms=10
    all_histos = takeAndReadAll64(s, intTime_ms)
    plot_histo(all_histos) 
    for i in range(len(csv_catcher)):
        count_data = pd.read_csv(i)
        time_series = count_data['# Counts vs Bin #']
        indices = find_peaks(time_series)[0]
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=time_series, mode='lines+markers', name='Original Plot'))
        fig.add_trace(go.Scatter(x=indices, y=[time_series[j] for j in indices], mode='markers', marker=dict(size=8,color='red',symbol='cross'),name='Detected Peaks'))
        fig.show()
        
def analyse_histo_tst2(s):
    intTime_ms=10
    all_histos = takeAndReadAll64(s, intTime_ms)
    plot_histo(all_histos) 
    csv = {}
        for i in range(1, 145):
            for j in range(1, 11):
                s = 'HMM_{}_{}'.format(i,j) 
                csv[s] = pd.read_csv(s+'.csv')
                time_series = csv[s](['# Counts vs Bin #'])
                indices = find_peaks(time_series)[0]
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=time_series, mode='lines+markers', name='Original Plot'))
                fig.add_trace(go.Scatter(x=indices, y=[time_series[j] for j in indices], mode='markers', marker=dict(size=8,color='red',symbol='cross'),name='Detected Peaks'))
                fig.show()

