tables = get_look_up_tables();
cp_table = tables{1};
ct_table = tables{2};
beta_vector = tables{4};
lambda_vector = tables{5};

tic

solutions = {};
ct_vector = {};
cp_vector = {};
lambda_opt = {};
beta_opt = {};
steps = 100000;
for k = 0:steps
    cp_ref = k * cp_max.Value/steps;
    cp_vector{end+1} =cp_ref;

    ct_best = inf;
    solutioni = NaN;
    for i = 1:length(lambda_vector)-1
        lambda = lambda_vector(i);
        lambda_plus1 = lambda_vector(i+1);
        for j = 1:length(beta_vector)-1
            beta = beta_vector(j);
            beta_plus1 = beta_vector(j+1);

            % getting the corner values of each tile

            % base
            cp_lambda_beta = table_look_up(cp_table,lambda_vector, beta_vector, lambda, beta);
            
            % one to beta and lambda respectively
            cp_lambda_beta_plus1 = table_look_up(cp_table,lambda_vector, beta_vector, lambda, beta_plus1);
            cp_lambda_plus1_beta = table_look_up(cp_table,lambda_vector, beta_vector, lambda_plus1, beta);
            cp_lambda_plus1_beta_plus1 = table_look_up(cp_table,lambda_vector, beta_vector, lambda_plus1, beta_plus1);

            % testing if the the target cp is contained in the tile ->
            % optimal value will always be on the boundary (4 line segments) of the tile
            % to check all segments it's enough to check only these two
            % assuming the optimal is not on the lines of (:, max(beta)),
            % (max(lambda), :)

            % 1. between (+0,+0) (+0,+1)
            if (cp_ref >= cp_lambda_beta && cp_ref <= cp_lambda_beta_plus1) || (cp_ref <= cp_lambda_beta && cp_ref >= cp_lambda_beta_plus1)
                r = abs((cp_ref - cp_lambda_beta_plus1)/(cp_lambda_beta_plus1 - cp_lambda_beta));
                lambda_sol = lambda;
                beta_sol = beta * r + beta_plus1 * (1-r);
                ct_sol = table_look_up(ct_table,lambda_vector, beta_vector, lambda_sol, beta_sol);
                if ct_sol < ct_best
                    solutioni = {lambda_sol, beta_sol};
                    ct_best = ct_sol;
                end
            end 
            

            % 2. between (+0, +0) (+1, +0)

            if (cp_ref >= cp_lambda_beta && cp_ref <= cp_lambda_plus1_beta) || (cp_ref <= cp_lambda_beta && cp_ref >= cp_lambda_plus1_beta)
                r = abs((cp_ref - cp_lambda_plus1_beta)/(cp_lambda_plus1_beta - cp_lambda_beta));
                lambda_sol = lambda * r + lambda_plus1 * (1-r);
                beta_sol = beta;
                ct_sol = table_look_up(ct_table,lambda_vector, beta_vector, lambda_sol, beta_sol);
                if ct_sol < ct_best
                    solutioni = {lambda_sol, beta_sol};
                    ct_best = ct_sol;
                end
            end

            % 3. between (0, +1) (+1, +1)

            if (cp_ref >= cp_lambda_plus1_beta_plus1 && cp_ref <= cp_lambda_beta_plus1) || (cp_ref <= cp_lambda_plus1_beta_plus1 && cp_ref >= cp_lambda_beta_plus1)
                r = abs((cp_ref - cp_lambda_plus1_beta_plus1)/(cp_lambda_beta_plus1 - cp_lambda_plus1_beta_plus1));
                lambda_sol = lambda * r + lambda_plus1 * (1-r);
                beta_sol = beta_plus1;
                ct_sol = table_look_up(ct_table,lambda_vector, beta_vector, lambda_sol, beta_sol);
                if ct_sol < ct_best
                    solutioni = {lambda_sol, beta_sol};
                    ct_best = ct_sol;
                end
            end 

            % 4. between (+1, 0) (+1, +1)

            if (cp_ref >= cp_lambda_plus1_beta_plus1 && cp_ref <= cp_lambda_plus1_beta) || (cp_ref <= cp_lambda_plus1_beta_plus1 && cp_ref >=  cp_lambda_plus1_beta)
                r = abs((cp_ref - cp_lambda_plus1_beta_plus1)/(cp_lambda_plus1_beta - cp_lambda_plus1_beta_plus1));
                lambda_sol = lambda_plus1;
                beta_sol = beta * r + beta_plus1 * (1-r);
                ct_sol = table_look_up(ct_table,lambda_vector, beta_vector, lambda_sol, beta_sol);
                if ct_sol < ct_best
                    solutioni = {lambda_sol, beta_sol};
                    ct_best = ct_sol;
                end
            end 





        end
    end
    solutions{end+1} = solutioni;
    lambda_opt{end+1} = solutioni{1};
    beta_opt{end+1} = solutioni{2};
    ct_vector{end+1} = ct_best;
end

for k = 1:length(solutions)
     solutionk = solutions{k};
     fprintf('lambda: %g, beta: %g, ct: %g\n', ...
        solutionk{1}, solutionk{2}, ct_vector{k});
end

save('xref_lookup.mat', 'solutions', 'ct_vector', 'cp_vector');

save('to_visulalize_xref.mat', 'lambda_opt', 'beta_opt', 'ct_vector', 'cp_vector');

toc