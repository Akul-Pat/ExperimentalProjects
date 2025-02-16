function root = secant_method(g, x0, x1, epsilon)
    % Input:
    % g: function handle for g(x)
    % x0: initial guess x^(-1)
    % x1: initial guess x^(0)
    % epsilon: tolerance for stopping criterion

    while true
        % Evaluate g at current and previous points
        g0 = g(x0);
        g1 = g(x1);

        % Compute the next approximation
        x_next = x1 - g1 * (x1 - x0) / (g1 - g0);

        % Check stopping criterion
        if abs(x_next - x1) < abs(x1) * epsilon
            root = x_next;
            return;
        end

        % Update variables for next iteration
        x0 = x1;
        x1 = x_next;
    end
end

% Define the function g(x)
g = @(x) (2*x - 1)^2 + 4*(4 - 1024*x)^4;

% Set initial guesses and parameters
x0 = 0;          % x^(-1)
x1 = 1;          % x^(0)
epsilon = 1e-5;  % Tolerance

% Call the secant method function
root = secant_method(g, x0, x1, epsilon);

% Display the result
fprintf('The root of g(x) is: %.6f\n', root);
fprintf('Value of g at the root: %.6e\n', g(root));