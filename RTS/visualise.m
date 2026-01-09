ct_array = cell2mat(ct_vector);

N = numel(ct_array);

lambda_array = zeros(1, N);
beta_array = zeros(1, N);

for k = 1:N
    lambda_array(k) = solutions{k}{1};
    beta_array(k) = solutions{k}{2};
end


cp_array = cell2mat(cp_vector);

ax1 = subplot(3,1,1);
scatter(cp_array, lambda_array, 10, '.', 'MarkerEdgeAlpha', 0.7);
xlabel('$c_p$', 'Interpreter', 'latex');
ylabel('$\lambda^{*}$', 'Interpreter', 'latex');
title('$\lambda^{*}$ vs $c_p$', 'Interpreter', 'latex');

% --- Second subplot: beta* vs c_p ---
ax2 = subplot(3,1,2);
scatter(cp_array, beta_array, 10, '.', 'MarkerEdgeAlpha', 0.7);
xlabel('$c_p$', 'Interpreter', 'latex');
ylabel('$\beta^{*}$', 'Interpreter', 'latex');
title('$\beta^{*}$ vs $c_p$', 'Interpreter', 'latex');

% --- Third subplot: c_t* vs c_p ---
ax3 = subplot(3,1,3);
scatter(cp_array, ct_array, 10, '.', 'MarkerEdgeAlpha', 0.7);
xlabel('$c_p$', 'Interpreter', 'latex');
ylabel('$c_t^{*}$', 'Interpreter', 'latex');
title('$c_t^{*}$ vs $c_p$', 'Interpreter', 'latex');



figure;
% --- Top plot: beta* vs lambda* colored by cp ---
nexttile;

% Define custom blue-to-red colormap
nColors = 256;
R = linspace(0.2, 0.7, nColors)';   % dark → moderate red
G = zeros(nColors,1);              % no green
B = linspace(0.7, 0.2, nColors)';  % dark → moderate blue

customMap = [R, G, B];

scatter(lambda_array, beta_array, 20, cp_array, 'filled'); % 20 = smaller point size
colormap(customMap);
colorbar;
caxis([min(cp_array), max(cp_array)]); % map full cp range to colormap
xlabel('$\lambda^{*}$', 'Interpreter','latex');
ylabel('$\beta^{*}$', 'Interpreter','latex');
title('$\beta^{*}$ vs $\lambda^{*}$ colored by $c_p$', 'Interpreter','latex');

% --- Overall title ---
sgtitle('$\beta^{*}$, $\lambda^{*}$ and $c_t^{*}$ visualisation', 'Interpreter','latex');
grid on;


figure;
hold on;
grid on;

scatter(cp_array, lambda_array, 10, '.', ...
    'MarkerEdgeAlpha', 0.7, ...
    'DisplayName', '$\lambda^{*}$');

scatter(cp_array, beta_array, 10, '.', ...
    'MarkerEdgeAlpha', 0.7, ...
    'DisplayName', '$\beta^{*}$');

scatter(cp_array, ct_array, 10, '.', ...
    'MarkerEdgeAlpha', 0.7, ...
    'DisplayName', '$c_t^{*}$');

xlabel('$c_p$', 'Interpreter', 'latex');
ylabel('Value', 'Interpreter', 'latex');
title('Optimal Variables vs $c_p$', 'Interpreter', 'latex');

legend('Interpreter', 'latex', 'Location', 'best');
hold off;