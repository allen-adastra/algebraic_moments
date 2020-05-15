# Algebraic-Moments

# Background
## Representing Moments with Multi-Indices

## Moment Bases

# Three Methods

## Moment Expressions
Letting $\mathbf{w}$ denote a random vector, $\mathbf{y}$ denote deterministic variables, and $g$ denote a polynomial function. The moment expressions capability allows the user to express:

$$\mathbb{E}[g(\mathbf{y}, \mathbf{w})^n]$$

in terms of moments of $\mathbf{y}$ and moments of $\mathbf{w}$ in closed form.

## Dynamical System Methods
Let $\mathbf{x}_t$ denote the state, $\mathbf{u}_t$ denote the control, and $\mathbf{w}_t$ denote a random vector that is independent of $\mathbf{x}_t$. The dynamical systems methods apply to sine-cosine polynomial systems:

$$\mathbf{x}_{t+1} = f(\mathbf{x}_t,\mathbf{w}_t, \mathbf{u}_t)$$
### 1) Moment Shooting
Suppose we want to find some moment of the state vector at some time step $T$: $\mathbb{E}[\mathbf{x}_T^\alpha]$. Moment shooting automatically expresses $\mathbb{E}[\mathbf{x}_T^\alpha]$ in terms of moments of $\mathbf{w}_{0:T-1}$ and moments of the initial state distribution $\mathbf{x}_0$.

### 2) Moment State Dynamical System
In contrast to the moment shooting method, the moment state dynamical system finds a new, higher dimensional dynamical system in terms of moment state. Suppose we are interested in the set of state moments $\mathbf{x}[\mathcal{A}]$. The moment state dynamical systems method uses an algorithm called TreeRing to find a completion $\bar{\mathcal{A}}$, a new system of equations, and a moment basis for the disturbance vector $\mathcal{B}$ such that:

$$\mathbf{x}_{t+1}[\mathcal{A}] = h(\mathbf{x}_t[\mathcal{A}],\mathbf{w}_t[\mathcal{B}], \mathbf{u}_t)$$


# Conventions
## Moment `string_rep`
- str(variable.string_rep) + str(variable.power)



## Variable Name Rules
 - No numbers
 - No subscripts
 - Only continuous letters