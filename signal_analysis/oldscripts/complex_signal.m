function complex_signal()

% define initial parameters: sampling frequency, time, frequencies
f_sample = 1000;
x_time = 0:1/f_sample:2;
freqs = [ .1 .5 3 5 10 12 25 30 45 ];
freqs_filt = [ 5 10 12 25 30 45];

% create complex signal

final_signal = do_signal(freqs, x_time)

% create filtered signal

final_signal_FILT = do_signal(freqs_filt, x_time)

plot(x_time, final_signal)
hold on
plot(x_time, final_signal_FILT)
legend('original', 'high-pass signal')

end

function out_signal = do_signal(freqs, x_time)

    n_freq = numel(freqs);
    eye_freq = repmat(freqs,n_freq,1).*eye(n_freq)*2*pi;
    time_freq_weighted = repmat(x_time',1,n_freq)*eye_freq;
    signals = sin(time_freq_weighted);
    out_signal = sum(signals,2);
    
end

